from nextflow import Pipeline
import os
import time
import subprocess
from nextflow.execution import Execution
from nextflow.utils import directory_is_ready, get_directory_id

class MyPipeline(Pipeline):
	
    def __init__(self, path, config=None):
        self.path = path
        self.config = config

    def __repr__(self):
        return f"<Pipeline ({self.path})>"

    @property
    def config_string(self):
        """Gets the full location of the config file as a command line
        argument.
        
        :rtype: ``str``"""
        
        if not self.config: return ""
        full_config_path = os.path.abspath(self.config)
        return f" -C \"{full_config_path}\""

    def run_and_poll(self, location=".", params=None, profile=None, version=None, sleep=5):
        """Runs the pipeline and creates :py:class:`.Execution` objects at
        intervals, returning them as a generator. You can specifiy where it will
        run, the command line parameters passed to it, the profile(s) it will
        run with, and the Nextflow version it will use.
        
        :param str location: the directory to run within and save outputs to.
        :param dict params: the parameters to pass at the command line.
        :param list profile: the names of profiles to use when running.
        :param str version: the Nextflow version to use.
        :param int sleep: the amount of time between Execution updates.
        :rtype: ``Execution``"""
        
        full_run_location = os.path.abspath(location)
        original_location = os.getcwd()
        command_string = self.create_command_string(params, profile, version) + "-resume"
        try:
            os.chdir(full_run_location)
            existing_id = get_directory_id(full_run_location)
            with open("nfstdout", "w") as fout:
                with open("nfstderr", "w") as ferr:
                    process = subprocess.Popen(
                        command_string, stdout=fout, stderr=ferr,
                        universal_newlines=True, shell=True,
                        cwd=full_run_location,
                    )
                    while True:
                        time.sleep(sleep)
                        returncode = process.poll()
                        with open("nfstdout") as f: out = f.read()
                        with open("nfstderr") as f: err = f.read()
                        if directory_is_ready(full_run_location, existing_id):
                            yield Execution.create_from_location(
                                full_run_location, self, out, err, returncode
                            )
                        if returncode is not None: break
        finally:
            if os.path.exists("nfstdout"): os.remove("nfstdout")
            if os.path.exists("nfstderr"): os.remove("nfstderr")
            os.chdir(original_location)

def run_and_poll(pipeline, config, *args, **kwargs):
    """Runs a pipeline by path and creates :py:class:`.Execution` objects at
    intervals, returning them as a generator. You can specifiy where it will
    run, the command line parameters passed to it, the profile(s) it will
    run with, and the Nextflow version it will use.
    
    :param str path: the path to the .nf file.
    :param str config: the path to the associated config file.
    :param str location: the directory to run within and save outputs to.
    :param dict params: the parameters to pass at the command line.
    :param list profile: the names of profiles to use when running.
    :param str version: the Nextflow version to use.
    :param int sleep: the amount of time between Execution updates.
    :rtype: ``Execution``"""
    
    print("AAAAA")
    pipeline = MyPipeline(path=pipeline, config=config)
    return pipeline.run_and_poll(*args, **kwargs)