using System.Linq;
using System.Collections.Generic;
using System.IO;
using System;

namespace Grammar
{
	public class GrammarImpl : IGrammar
	{

        public IList<Terminal> Terminals { get; } = new List<Terminal>();
		public Terminal? AddTerminal(string name)
		{
			if (!Terminals.Any(x => x.Name == name)) Terminals.Add(new Terminal(name));

			return Terminals.FirstOrDefault(x => x.Name == name);
		}

		public IList<Nonterminal> Nonterminals { get; } = new List<Nonterminal>();

		public Nonterminal? AddNonterminal(string name)
		{
		    if (!Nonterminals.Any(x => x.Name == name)) Nonterminals.Add(new Nonterminal(name));
			
			return Nonterminals.FirstOrDefault(x=>x.Name == name);
		}

		public IList<Rule> Rules
		{
			get
			{
				List<Rule> rules = new List<Rule>();
				foreach (Nonterminal nt in Nonterminals)
				{
					foreach (Rule rule in nt.Rules)
					{
						rules.Add(rule);
					}
				}
				return rules;
			}
		}

		public Nonterminal? StartingNonterminal { get; set; } 

		public void dump()
		{
			Console.WriteLine("Terminals:");
		    foreach ( Terminal t in  Terminals) {
				Console.Write(" "+t.Name);
			}
			Console.WriteLine("\nNonterminals:");

			foreach ( Nonterminal nt in Nonterminals) {
				Console.Write(" "+nt.Name);
			}
			Console.WriteLine();

			Console.WriteLine("Starting nonterminal: "+StartingNonterminal?.Name);

			Console.WriteLine("Rules:");
		    int i = 0;
			foreach (Rule rule in Rules) {
			    i++;
				Console.Write("[" + i + "] " + rule.LHS.Name+" -> ");

			    foreach (Symbol symbol in rule.RHS)
			    {
			        Console.Write(symbol.Name+" ");
				}
				Console.WriteLine();
			}
		}
	}
}