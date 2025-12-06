class DNAOneTimeTask:

    def run(self):
        self.executor.interaction.activate()
        self.sleep(0.5)
        self.setup_jitter()
