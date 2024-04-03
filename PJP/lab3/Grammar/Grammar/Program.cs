using Grammar;
using System;
using System.IO;

namespace Lab3
{

	class Program
	{
		static void Main(string[] args)
		{
			try
			{
				StreamReader r = new StreamReader(new FileStream("G1.TXT", FileMode.Open));

				GrammarReader inp = new GrammarReader(r);
				var grammar = inp.Read();
				grammar.dump();

				GrammarOps gr = new GrammarOps(grammar);

				// First step, computes nonterminals that can be rewritten as empty word
				foreach (Nonterminal nt in gr.EmptyNonterminals)
				{
					Console.Write(nt.Name + " ");
				}
				Console.WriteLine();
			}
			catch (GrammarException e)
			{
				Console.WriteLine($"{e.LineNumber}: Error -  {e.Message}");
			}
			catch (IOException e)
			{
				Console.WriteLine(e);
			}
		}
	}
}