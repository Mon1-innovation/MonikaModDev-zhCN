init -999:
    default persistent._mas_submod_version_data = dict()

init 10 python:
    #Run updates if need be
    store.mas_submod_utils.Submod._checkUpdates()

init -989 python:
    #Log initialized submods
    if store.mas_submod_utils.Submod.hasSubmods():
        mas_submod_utils.submod_log.info(
            "\nINSTALLED SUBMODS:\n{0}".format(
                ",\n".join(
                    [
                        "    '{0}' v{1}".format(submod.name, submod.version)
                        for submod in store.mas_submod_utils.Submod.getSubmods()
                    ]
                )
            )
        )

    #Run dependency checks
    store.mas_submod_utils.Submod._checkDependencies()

init -991 python in mas_submod_utils:
    import re
    import os
    import json
    # import sys
    # import traceback
    from urllib.parse import urlparse

    import store
    from store import (
        config,
        persistent,
        mas_utils,
        mas_logging
    )


    submod_log = mas_logging.init_log("submod_log")

    # NOTE: ALWAYS UPDATE VERSION IF YOU CHANGE HEADER FORMAT
    # That way we can keep things compatible!
    HEADER_VERSION = 1
    HEADER_JSON_FN = "header.json"
    # The directories we're checking for submods, relative to `game/`
    SUBMOD_DIRS = [
        "Submods/"
    ]


    def _read_submod_header(path: str) -> dict|None:
        """
        Tries to read a submod header at the given path

        IN:
            path - str, abs path to the submod
        """
        header_path = os.path.join(path, HEADER_JSON_FN)
        if not os.path.exists(header_path):
            return None

        header_json = None
        last_err = None
        try:
            with open(header_path) as header_file:
                header_json = json.load(header_file)

        except Exception as last_err:
            pass

        if not header_json:
            submod_log.error(
                "Found submod header, but couldn't read it: '{}'".format(path),
                exc_info=(last_err is not None)
            )
            return None

        return header_json

    def _process_submod_header(header_json: dict, path: str) -> bool:
        """
        This does extra processing on header, like setting default values
        if optional parameters not present

        IN:
            header_json - dict, the parsed submod json
            path - str, abs path to the submod

        OUT:
            boolean - True if successfully, False otherwise
        """
        # NOTE: pop from the dict sinse it's not used in the submod constructor
        v = header_json.pop("header_version", None)
        if v is None:
            submod_log.error(
                "Submod is missing required 'header_version' field: '{}'".format(path)
            )
            return False

        # NOTE: for now we just don't load outdated headers,
        # but we could try to process old headers in the future if
        # we decide we want to do so
        if v < HEADER_VERSION:
            submod_log.error(
                "Submod has outdated header version (expected {}, got {}): '{}'".format(
                    HEADER_VERSION,
                    v,
                    path
                )
            )
            return False

        # header_json.setdefault("description", "")
        # header_json.setdefault("dependencies", None)
        # header_json.setdefault("settings_pane", None)
        # header_json.setdefault("version_updates", {})
        # header_json.setdefault("coauthors", ())
        # header_json.setdefault("repository", "")
        # header_json.setdefault("priority", 0)

        return True

    def _load_submod(path: str):
        """
        Reads a submod json header at the given path,
        validates and and tries to load the submod

        IN:
            path - str, abs path to the submod location
        """
        if not (header_json := _read_submod_header(path)):
            return

        if not _process_submod_header(header_json, path):
            return

        try:
            submod_obj = Submod(**header_json)

        except (SubmodError, TypeError) as e:# TypeError is for extra/invalid args
            submod_log.error(
                "Invalid submod found at: '{}'".format(path),
                exc_info=True
            )

        except Exception as e:
            submod_log.critical(
                "Critical error while validating submod at: '{}'".format(path),
                exc_info=True,
                stack_info=True
            )

    def _load_submods():
        """
        Scans and loads submods
        """
        for submod_dir in SUBMOD_DIRS:
            path = os.path.join(config.gamedir, submod_dir)
            for entry in os.scandir(path):
                if entry.is_dir():
                    _load_submod(entry.path)


    class SubmodError(Exception):
        def __init__(self, _msg):
            self.msg = _msg
        def __str__(self):
            return self.msg

    class Submod(object):
        """
        Submod class

        PROPERTIES:
            author - submod author
            name - submod name
            version - version of the submod installed
            description - submod description
            dependencies - dependencies required for the submod
            settings_pane - string referring to the screen used for the submod's settings
            version_updates - update labels
        """
        #The fallback version string, used in case we don't have valid data
        FB_VERS_STR = "0.0.0"

        #Regular expression representing a valid author and name
        AN_REGEXP = re.compile(r'^[a-zA-Z_\u00a0-\ufffd][ 0-9a-zA-Z_\u00a0-\ufffd]*$')

        _submod_map = dict()

        def __init__(
            self,
            author,
            name,
            version,
            modules,
            description="",
            dependencies=None,
            settings_pane=None,
            version_updates={},
            coauthors=(),
            repository="",
            priority=0,
        ):
            """
            Submod object constructor

            IN:
                author - string, author name.

                name - submod name

                version - version number in format SPECIFICALLY like so: `1.2.3`
                    (You can add more or less as need be, but splits MUST be made using periods)

                modules - list of modules of this submod

                description - a short description for the submod
                    (Default: "")

                dependencies - dictionary in the following structure: {"name": ("minimum_version", "maximum_version")}
                corresponding to the needed submod name and version required
                NOTE: versions must be passed in the same way as the version property is done
                    (Default: empty dict)

                settings_pane - a string representing the screen for this submod's settings
                    (Default: None)

                version_updates - dict of the format {"old_version_update_label_name": "new_version_update_label_name"}
                    NOTE: submods MUST use the format <author>_<name>_v<version> for update labels relating to their submods
                    NOTE: capital letters will be forced to lower and spaces will be replaced with underscores
                    NOTE: Update labels MUST accept a version parameter, defaulted to the version of the label
                    For example:
                        author name: MonikaAfterStory,
                        submod name: Example Submod
                        submod vers: 1.2.3

                    becomes:
                        label monikaafterstory_example_submod_v1_2_3(version="v1_2_3")

                coauthors - tuple of co-authors of this submod
                    (Default: empty tuple)

                repository - link to the submod repository
                    (Default: "")

                priority - submod loading priority. Must be within -999 and 999
                    (Default: 0)
            """
            #First make sure this name us unique
            if name in self._submod_map:
                raise SubmodError("A submod with name '{}' has been installed twice. Please, uninstall the duplicate.".format(name))

            #Now we verify that the version number is something proper
            if not self._isValidVersion(version):
                raise SubmodError("Version number '{}' is invalid.".format(version))

            #Make sure author and name are proper label names
            if not Submod.AN_REGEXP.match(author):
                raise SubmodError("Author '{0}' is invalid.".format(author))
            if not Submod.AN_REGEXP.match(name):
                raise SubmodError("Name '{0}' is invalid.".format(name))

            if not isinstance(description, str):
                raise SubmodError("Description '{0}' is invalid.".format(description))

            if dependencies is not None:
                if not isinstance(dependencies, (dict, python_dict)):
                    raise SubmodError("Invalid 'dependencies' field for the submod '{}'.".format(name))

                for k, v in dependencies.items():
                    if not isinstance(k, str):
                        raise SubmodError("Invalid key '{}' in the 'dependencies' field for the submod '{}'.".format(k, name))

                    if not isinstance(v, (tuple, list, python_list)):
                        raise SubmodError("Invalid value type for key '{}' in the 'dependencies' field for the submod '{}'.".format(k, name))

                    if len(v) != 2:
                        raise SubmodError("Invalid value for key '{}' in the 'dependencies' field for the submod '{}'.".format(k, name))

                    for i in v:
                        if not self._isValidVersion(i):
                            raise SubmodError("Invalid value for key '{}' in the 'dependencies' field for the submod '{}'.".format(k, name))

            else:
                dependencies = {}

            if settings_pane is not None and not isinstance(settings_pane, str):
                raise SubmodError("Invalid 'settings_pane' field for the submod '{}'.".format(name))

            if repository:
                url = urlparse(repository)
                if url.scheme != "https":
                    submod_log.warning("Submod '{}' doesn't use https scheme in its repository link")
                if url.netloc != "github.com":
                    submod_log.warning("Submod '{}' uses unknown repository hosting. Consider switching to GitHub.com")
                elif (
                    url.path.count("/") != 2
                    or url.params
                    or url.query
                    or url.fragmnent
                ):
                    # Only for github
                    submod_log.warning("Submod '{}' seems to have invalid link to the repository.")

            if not isinstance(priority, int) or not (-999 <= priority <= 999):
                raise SubmodError("Invalid 'priority' field for the submod '{}'.".format(name))

            #With verification done, let's make the object
            self.author = author
            self.name = name
            self.version = version
            self.modules = modules
            self.description = description
            self.dependencies = dependencies
            self.settings_pane = settings_pane
            self.version_updates = version_updates
            self.coauthors = tuple(coauthors)
            self.repository = repository
            self.priority = priority

            #Now we add these to our maps
            self._submod_map[name] = self

            #NOTE: We check for things having updated later so all update scripts get called together
            if name not in persistent._mas_submod_version_data:
                persistent._mas_submod_version_data[name] = version

        def __repr__(self):
            """
            Representation of this object
            """
            return "<Submod: ({0} v{1} by {2})>".format(self.name, self.version, self.author)

        def getVersionNumberList(self):
            """
            Gets the version number as a list of integers

            OUT:
                List of integers representing the version number
            """
            return list(self._parseVersions(self.version))

        def hasUpdated(self):
            """
            Checks if this submod instance was updated (version number has incremented)

            OUT:
                boolean:
                    - True if the version number has incremented from the persistent one
                    - False otherwise
            """
            old_vers = persistent._mas_submod_version_data.get(self.name)

            #If we don't have an old vers, we're installing for the first time and aren't updating at all
            if not old_vers:
                return False

            try:
                old_vers = list(self._parseVersions(old_vers))

            #Persist data was bad, we'll replace it with something safe and return False as we need not check more
            except:
                persistent._mas_submod_version_data[self.name] = Submod.FB_VERS_STR
                return False

            return self.checkVersions(old_vers) > 0

        def updateFrom(self, version):
            """
            Updates the submod, starting at the given start version

            IN:
                version - the version number in the parsed format ('author_name_v#_#_#')
            """
            while version in self.version_updates:
                updateTo = self.version_updates[version]

                # we should only call update labels that we have
                if renpy.has_label(updateTo) and not renpy.seen_label(updateTo):
                    renpy.call_in_new_context(updateTo, updateTo)
                version = self.version_updates[version]

        def checkVersions(self, comparative_vers):
            """
            Generic version checker for submods

            IN:
                curr_vers - current installed version of the submod as a list
                comparative_vers - the version we're comparing to (or need the current version to be at or greater than) as a list

            OUT:
                integer:
                    - (-1) if the current version number is less than the comparitive version
                    - 0 if the current version is the same as the comparitive version
                    - 1 if the current version is greater than the comparitive version
            """
            return mas_utils.compareVersionLists(
                self.getVersionNumberList(),
                comparative_vers
            )

        @classmethod
        def _checkUpdates(cls):
            """
            Checks if submods have updated and sets the appropriate update scripts for them to run
            """
            #Iter thru all submods we've got stored
            for submod in cls.getSubmods():
                #If it has updated, we need to call their update scripts and adjust the version data value
                if submod.hasUpdated():
                    submod.updateFrom(
                        "{0}_{1}_v{2}".format(
                            submod.author,
                            submod.name,
                            persistent._mas_submod_version_data.get(submod.name, Submod.FB_VERS_STR).replace('.', '_')
                        ).lower().replace(' ', '_')
                    )

                #Even if this hasn't updated, we should adjust its value to reflect the correct version
                persistent._mas_submod_version_data[submod.name] = submod.version

        @staticmethod
        def _parseVersions(version):
            """
            Parses a string version number to list format.

            IN:
                version - version string to parse

            OUT:
                tuple - representing the parsed version number

            NOTE: Does not handle errors as to get here, formats must be correct regardless
            """
            return tuple(map(int, version.split('.')))

        @classmethod
        def _isValidVersion(cls, version):
            """
            Checks if the given version string has valid format

            IN:
                version - version string to test

            OUT:
                boolean
            """
            try:
                cls._parseVersions(version)
            except ValueError:
                return False

            return True

        @classmethod
        def _checkDependencies(cls):
            """
            Checks to see if the dependencies for this submod are met
            """
            for submod in cls.getSubmods():
                for dependency, minmax_version_tuple in submod.dependencies.items():
                    dependency_submod = Submod._getSubmod(dependency)

                    if dependency_submod is not None:
                        #Now we need to split our minmax
                        minimum_version, maximum_version = minmax_version_tuple

                        #First, check the minimum version. If we get -1, we're out of date
                        if (
                            minimum_version
                            and dependency_submod.checkVersions(cls._parseVersions(minimum_version)) < 0
                        ):
                            raise SubmodError(
                                "Submod '{0}' is out of date. Version {1} required for {2}. Installed version is {3}".format(
                                    dependency_submod.name, minimum_version, submod.name, dependency_submod.version
                                )
                            )

                        #If we have a maximum version, we should check if we're above it.
                        #If we get 1, this is incompatible and we should crash to avoid other ones
                        elif (
                            maximum_version
                            and dependency_submod.checkVersions(cls._parseVersions(maximum_version)) > 0
                        ):
                            raise SubmodError(
                                "Version '{0}' of '{1}' is installed and is incompatible with {2}.\nVersion {3} is compatible.".format(
                                    dependency_submod.version, dependency_submod.name, submod.name, maximum_version
                                )
                            )

                    #Submod wasn't installed at all
                    else:
                        raise SubmodError(
                            "Submod '{0}' is not installed and is required for {1}.".format(
                                dependency, submod.name
                            )
                        )

        @classmethod
        def hasSubmods(cls):
            """
            Checks if any submods were loaded

            OUT:
                bool
            """
            return bool(cls._submod_map)

        @classmethod
        def _getSubmod(cls, name):
            """
            Gets the submod with the name provided

            IN:
                name - name of the submod to get

            OUT:
                Submod object representing the submod by name if installed and registered
                None if not found
            """
            return cls._submod_map.get(name)

        @classmethod
        def getSubmods(cls):
            """
            Returns all the submods

            OUT:
                iterable of Submod objects
            """
            return cls._submod_map.values()

    #END: Submod class
    def isSubmodInstalled(name, version=None):
        """
        Checks if a submod with `name` is installed

        IN:
            name - name of the submod to check for
            version - if a specific version (or greater) is installed
            (NOTE: if None, this is ignored. Default: None)

        OUT:
            boolean:
                - True if submod with name is installed
                - False otherwise
        """
        submod = Submod._getSubmod(name)

        if submod and version:
            return submod.checkVersions(version) >= 0
        return bool(submod)

#START: Function Plugins
init -980 python in mas_submod_utils:
    import inspect
    import store

    #Store the current label for use elsewhere
    current_label = None
    #Last label
    last_label = None

    #Dict of all function plugins
    function_plugins = dict()

    #Default priority
    DEF_PRIORITY = 0

    #Priority for jumps and calls
    JUMP_CALL_PRIORITY = 999

    PRIORITY_SORT_KEY = lambda x: x[1][2]

    #START: Decorator Function
    def functionplugin(_label, _args=[], auto_error_handling=True, priority=0):
        """
        Decorator function to register a plugin

        The same as registerFunction. See its doc for parameter details
        """
        def wrap(_function):
            registerFunction(
                _label,
                _function,
                _args,
                auto_error_handling,
                priority
            )
            return _function
        return wrap

    #START: Internal functions
    def getAndRunFunctions(key=None):
        """
        Gets and runs functions within the key provided

        IN:
            key - Key to retrieve and run functions from
        """
        global function_plugins

        #If the key isn't provided, we assume it from the caller
        if not key:
            key = inspect.stack()[1][3]

        func_dict = function_plugins.get(key)

        if not func_dict:
            return

        #Firstly, let's get our sorted list
        sorted_plugins = __prioritySort(key)
        for _action, data_tuple in sorted_plugins:
            if data_tuple[1]:
                try:
                    store.__run(_action, getArgs(key, _action))
                except Exception as ex:
                    store.mas_utils.mas_log.error("function {0} failed because {1}".format(_action.__name__, ex))

            else:
                store.__run(_action, getArgs(key, _action))

    def registerFunction(key, _function, args=[], auto_error_handling=True, priority=DEF_PRIORITY):
        """
        Registers a function to the function_plugins dict

        NOTE: Does NOT allow overwriting of existing functions in the dict
        NOTE: Function must be callable
        NOTE: Functions run when a label matching the key for the function is:
        called, jumped, or fallen through to.
        Or if plugged into a function, when a function by the name of the key calls getAndRunFunctions

        IN:
            key - key to add the function to.
                NOTE: The key is either a label, or a function name
                NOTE: Function names only work if the function contains a getAndRunFunctions call.
                    Without it, it does nothing.
            _function - function to register
            args - list of args (must be in order) to pass to the function
                (Default: [])
            auto_error_handling - whether or function plugins should ignore errors in functions
                (Set this to False for functions which call or jump)
            priority - Order priority to run functions
                (Like init levels, the lower the number, the earlier it runs)

        OUT:
            boolean:
                - True if the function was registered successfully
                - False otherwise
        """
        global function_plugins

        #Verify that the function is callable
        if not callable(_function):
            store.mas_utils.mas_log.error("{0} is not callable".format(_function.__name__))
            return False

        #Too many args
        elif len(args) > len(inspect.getargspec(_function).args):
            store.mas_utils.mas_log.error("Too many args provided for function {0}".format(_function.__name__))
            return False

        #Check for overrides
        key = __getOverrideLabel(key)

        #Create the key if we need to
        if key not in function_plugins:
            function_plugins[key] = dict()

        #If we just created a key, then there won't be any existing values so we elif
        elif _function in function_plugins[key]:
            return False

        function_plugins[key][_function] = (args, auto_error_handling, priority)
        return True

    def getArgs(key, _function):
        """
        Gets args for the given function at the given key

        IN:
            key - key to retrieve the function from
            _function - function to retrieve args from

        OUT:
            list of args if the function is present
            If function is not present, None is returned
        """
        global function_plugins

        func_dict = function_plugins.get(key)

        if not func_dict:
            return

        return func_dict.get(_function)[0]

    def setArgs(key, _function, args=[]):
        """
        Sets args for the given function at the key

        IN:
            key - key that the function's function dict is stored in
            _function - function to set the args
            args - list of args (must be in order) to pass to the function (Default: [])

        OUT:
            boolean:
                - True if args were set successfully
                - False if not
        """
        global function_plugins

        func_dict = function_plugins.get(key)

        #Key doesn't exist
        if not func_dict:
            return False

        #Function not in dict
        elif _function not in func_dict:
            return False

        #Too many args provided
        elif len(args) > len(inspect.getargspec(_function).args):
            store.mas_utils.mas_log.error("Too many args provided for function {0}".format(_function.__name__))
            return False

        #Otherwise we can set
        old_values = func_dict[_function]
        func_dict[_function] = (args, old_values[1], old_values[2])
        return True

    def unregisterFunction(key, _function):
        """
        Unregisters a function from the function_plugins dict

        IN:
            key - key the function we want to unregister is in
            _function - function we want to unregister

        OUT:
            boolean:
                - True if function was unregistered successfully
                - False otherwise
        """
        global function_plugins

        func_dict = function_plugins.get(key)

        #Key doesn't exist
        if not func_dict:
            return False

        #Function not in plugins dict
        elif _function not in func_dict:
            return False

        #Otherwise we can pop
        function_plugins[key].pop(_function)
        return True

    def __prioritySort(_label):
        """
        Sorts function plugins based on the priority order system

        IN:
            _label - label to sort functions by priority for

        OUT:
            sorted list of (_function, data_tuple) tuples

        NOTE: This assumes that the label exists in the function_plugins dict
        """
        global function_plugins

        #First, we need to convert the functions into a list of tuples
        func_list = [
            (_function, data_tuple)
            for _function, data_tuple in function_plugins[_label].items()
        ]

        return sorted(func_list, key=PRIORITY_SORT_KEY)

    def __getOverrideLabel(_label):
        """
        Gets the override label for the given label (will follow the chain if overrides are overridden)

        IN:
            _label - label to get the override label for

        OUT:
            string representing the last label in the override chain or _label if there are no overrides
        """
        while renpy.config.label_overrides.get(_label) is not None:
            _label = renpy.config.label_overrides[_label]
        return _label

#Global run area
init -990 python:
    def __run(_function, args):
        """
        Private function to run a function in the global store
        """
        return _function(*args)

#Label callback to get last label and run function plugins from the label
init 999 python:
    def label_callback(name, abnormal):
        """
        Function to run plugin functions and store the last label
        """
        #First, update the last label to what was current
        store.mas_submod_utils.last_label = store.mas_submod_utils.current_label
        #Now we can update the current
        store.mas_submod_utils.current_label = name
        #Run functions
        store.mas_submod_utils.getAndRunFunctions(name)

        #Let's also check if the current label is an override label, if so, we'll then mark the base label as seen
        base_label = _OVERRIDE_LABEL_TO_BASE_LABEL_MAP.get(name)
        if base_label is not None:
            persistent._seen_ever[base_label] = True

    config.label_callback = label_callback

    @store.mas_submod_utils.functionplugin("ch30_reset", priority=-999)
    def __build_override_label_to_base_label_map():
        """
        Populates a lookup dict for all label overrides which are in effect
        """
        #Let's loop here to update our label overrides map
        for overridden_label, label_override in config.label_overrides.items():
            _OVERRIDE_LABEL_TO_BASE_LABEL_MAP[label_override] = overridden_label
