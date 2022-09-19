from ipykernel.kernelbase import Kernel


class MyEchoKernel(Kernel):
    implementation = "RhGoyalEcho"
    implementation_version = "1.0"
    language = "no-op"
    language_version = "1.0"
    language_info = {
        "name": "Any text",
        "mimetype": "text/plain",
        "file_extension": ".txt",
    }
    banner = "A ipython wrapper Echo Kernel - for Demo"

    def do_execute(
        self, code, silent, store_history=True, user_expressions=None, allow_stdin=False
    ):
        print("execute....")
        if not silent:
            print("Received: {}".format(code))
            stream_context = {"name": "stdout", "text": code}
            self.send_response(self.iopub_socket, "stream", stream_context)
        print("returning...")
        return {
            "status": "ok",
            # The base class increments the execution count
            "execution_count": self.execution_count,
            "payload": [],
            "user_expressions": {},
        }

    def do_shutdown(self, restart):
        print("Executing shutdown hook...")
        # super(MyEchoKernel, self).do_shutdown(restart)


if __name__ == "__main__":
    from ipykernel.kernelapp import IPKernelApp

    print("starting kernel application instance..")
    IPKernelApp.launch_instance(kernel_class=MyEchoKernel)
