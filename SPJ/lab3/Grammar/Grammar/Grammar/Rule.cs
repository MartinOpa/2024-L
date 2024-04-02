using System.Collections.Generic;

namespace Grammar
{

	public class Rule
	{

		public Rule(Nonterminal lhs)
		{
			this.LHS = lhs;
		}

		public Nonterminal LHS { get; init; }

		public IList<Symbol> RHS { get; } = new List<Symbol>();
	}
}