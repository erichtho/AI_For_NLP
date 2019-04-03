"""
自测题三
"""

import random
class SenctenceGenerator():
    def __init__(self, grammar=None):
        self.grammar = """
        sentence => noun_phrase verb_phrase 
        noun_phrase => Article Adj* noun
        Adj* => null | Adj Adj*
        verb_phrase => verb noun_phrase
        Article => 一个 | 这个
        noun => 女人| 篮球|桌子|小猫
        verb => 看着 | 听着 | 看见
        Adj=> 蓝色的| 好看的|小小的|年轻的 
        """ if grammar is None else grammar

        self.grammar_dict = dict([tuple([w.strip() for w in gram.strip().split('=>')])  for gram in self.grammar.strip().split('\n')])
        for p in self.grammar_dict:
            self.grammar_dict[p] = [[w.strip() for w in choice.strip().split()] for choice in self.grammar_dict[p].split('|')]



    def generate(self, part):
        if part in self.grammar_dict:
            g = self.grammar_dict[part]
            unit_list = random.choice(g)
            return ''.join([self.generate(unit) for unit in unit_list])
        elif part=='null':
            return ''
        else:
        	return part


if __name__=='__main__':
    sg = SenctenceGenerator()
    print(''.join([s for s in sg.generate('noun_phrase')]))

    
