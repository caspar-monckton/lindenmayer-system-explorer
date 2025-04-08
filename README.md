# Lindenmayer System Explorer

## About

Lindenmayer systems (L-systems for short) are a type of formal grammar consisting of rewriting rules that operate on strings. They consist of a set of transformations that take a symbol (or set of symbols) as an input and transform it into a different set of symbols. Crucially, all symbols in a string are replaced using the relevant rules each iteration, whereas more traditional rewriting rules rewrite strings term by term or using other algorithms.

We distinguish between "context free" and "context dependent" L-systems. a context free L-system simply applies a rewriting rule whenever the input of the rule matches the current symbol. A context dependent L-system on the other hand can check the neighbours around a symbol to see if they match a certain set of symbols in a rule. Crucially, when the replacement is made, only the symbol of interest is replaced - those symbols forming a neighbourhood are left untouched by this particular map (though may be modified by a separate rule in the set of rewriting rules).

Context dependent L-systems can be thought of as a powerful generalisation of cellular automata. Whereas a cellular automata can only change the state of a single cell based on its neighbours, a context dependent L-system can create multiple cells in the place of an old cell according to its neighbours. Cellular automata are simply context dependent L-systems where the replacement is the same length as the original input.

## Usage

lindenInterpreter.py spins up a text based interface with which you can create, save, read, and run L-systems on specific input seeds. It has support for regular, context-dependent and even stochastic L-systems (where rules are multifunctions). run lindenInterpreter.py and then type "h" for information on what commands are available.
