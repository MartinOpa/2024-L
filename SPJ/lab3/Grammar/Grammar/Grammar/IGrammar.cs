using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
namespace Grammar
{
    public interface IGrammar
    {
        IList<Nonterminal> Nonterminals { get; }

        IList<Terminal> Terminals { get; }
        IList<Rule> Rules { get; }

        Nonterminal? StartingNonterminal { get;  }

        void dump();
    }
}