using System;
using System.Collections.Generic;
namespace Grammar
{
	public class Nonterminal : Symbol
	{
		public Nonterminal(string name) : base(name)
		{
		}
		public IList<Rule> Rules { get; } = new List<Rule>();
		public void AddRule(Rule rule)
		{
			Rules.Add(rule);
		}
	}
}