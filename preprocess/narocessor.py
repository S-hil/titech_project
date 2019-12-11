import json
import logging

logging.basicConfig(format='[%(levelname)s] %(name)s: %(message)s',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

class Processor(object):
    def __init__(self, stream_in, stream_out):
        """ Initialize and reset this instance
        Args:
            stream_in  : Input stream
            stream_out : Output stream
        """
        self.stream_in = stream_in
        self.stream_out = stream_out
        # Output JSON meta info
        self.stream_out.write(
            self.stream_in.readline()
        )

    def preprocess(self):
        """ Process input lines and output results
        This method reads input stream line by line and
        passes them to _preprocess, which formats a line
        and returns one or more formatted sentences.
        (Be noticed line may contain multiple sentences.)
        """
        while True:
            line = self.stream_in.readline()
            if line == '': break
            
            logger.info("Processing: {}".format(line.strip()))
            
            for sentence in self._preprocess(line.strip()):
                self.stream_out.write(sentence + '\n')

    def _preprocess(self, line):
        """ Yield formatted sentences
        Args:
            line (str): A line of sentence(s)

        Yields:
            str: Formatted sentence
        """
        # Remove unnecessary symbols
        line = self._remove_trash(line)

        # Register newly found kaomoji and replace them into id
        line = self._extract_kaomoji(line)
        
        # Process conversation
        # for sentence in self._preprocess()

        # Split a line into one or more sentences
        for sentence in self._split_line(line):
            yield sentence

    def _remove_trash(self, line):
        logger.warning("Not implemented yet")
        return line

    def _extract_kaomoji(self, line):
        logger.warning("Not implemented yet")
        return line

    def _split_line(self, line):
        logger.warning("Not implemented yet")
        return [line]
