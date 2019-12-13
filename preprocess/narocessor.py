# coding: utf-8
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
        for block in self._process_conversations(line):
            # Split line into sentences
            for sentence in self._split_line(block):
                if sentence != '':
                    yield sentence

    def _remove_trash(self, line):
        """ Remove unnecessary line and characters
        Args:
            line(str) : Line of sentences

        Returns:
            str: Line with uncecessary characters removed
        """
        whitespaceList = [' ', '　']
        seperaterList = [
            '-', '=', '*', '~', '+', '/', '\\',
            'ー', '＝', '＊', '〜', '＋', '／', '＼',
            '★', '☆', '●', '○', '◎',
            '◆', '◇', '■', '□', '❏', '❐',
            '▲', '△', '▼', '▽', '▶', '▷', '◀', '◁',
            '♠', '♤', '♦', '♢', '♣', '♧', '♥', '♡',
            '✤'
        ]

        # remove whitespaces
        chars = line
        for whitespace in whitespaceList:
            chars = chars.replace(whitespace, '')

        # check if `chars` consists of seperater
        for c in chars:
            if c not in seperaterList:
                break
        else:
            return ''
        
        return line.strip()

    def _extract_kaomoji(self, line):
        logger.warning("Not implemented yet")
        return line

    def _process_conversations(self, line):
        """ Extract conversations and pass them to _preprocess
        """
        bracketsList = [
            ('「', '」'), ('『', '』'), ('【', '】'),
            ('（', '）'), ('［', '］'), ('〈', '〉'),
            ('｛', '｝'), ('《', '》'), ('〔', '〕'),
            ('〘', '〙'), ('〚', '〛'), ('«', '»'),
            ('”', '”'), ('"', '"'), ('“', '”'),
            ('(', ')'), ('[', ']'), ('<', '>'),
        ]
        beginTalk = False
        bracketType = None
        newLine = ''
        
        for c in line:
            for brackets in bracketsList:
                if not beginTalk and c == brackets[0]:
                    # found the beginning of conversation
                    yield newLine
                    yield brackets[0]
                    beginTalk = True
                    bracketType = brackets[1]
                    newLine = ''
                    break
                
                elif beginTalk and c == bracketType:
                    # found the end of conversation
                    # we need to preprocess this line recursively
                    # since it's conversation
                    yield newLine
                    #for sentence in self._preprocess(newLine):
                    #    yield sentence
                    yield bracketType
                    beginTalk = False
                    newLine = ''
                    break
            else:
                # if c is not a bracket
                newLine += c
        
        yield newLine

    def _split_line(self, line):
        logger.warning("Not implemented yet")
        return [line]
