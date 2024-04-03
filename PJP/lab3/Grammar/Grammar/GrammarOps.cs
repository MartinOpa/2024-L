using Grammar;
using System.Collections.Generic;
using System;
using System.Linq;

namespace Lab3
{
	public class GrammarOps
	{
		public GrammarOps(IGrammar g)
		{
			this.g = g;
			compute_empty();
		}

		public ISet<Nonterminal> EmptyNonterminals { get; } = new HashSet<Nonterminal>();
		private void compute_empty()
		{
			List<string> chars = new List<string>{};
			foreach (Symbol sym in g.Nonterminals) {
				chars.Add(sym.Name);
			}

			chars.Sort();

			List<string> nonterminals = new List<string>{};
			List<string> terminals = new List<string>{};
			List<string> nonterminalsEpsilon = new List<string>{};
			foreach (string sym in chars) {
				if (sym.Equals(sym.ToLower())) {
					terminals.Add(sym.Trim());
				} else {
					nonterminals.Add(sym.Trim());
				}
			}

			int rows = nonterminals.Count + 1;
			int cols = nonterminals.Count + terminals.Count + 1;

        	string[,] symbols = new string[rows, cols];
			
			for (int i = 1; i < rows; i++) {
				symbols[i, 0] = nonterminals[i - 1];
			}

			for (int i = 1; i < rows; i++) {
				symbols[0, i] = nonterminals[i - 1];
			}

			for (int i = rows; i < cols; i++) {
				symbols[0, i] = terminals[i - rows];
			}

			for (int i = 0; i < nonterminals.Count; i++) {
				foreach (Rule rule in g.Rules) {
					if (rule.RHS.Count == 0 && !nonterminalsEpsilon.Contains(rule.LHS.Name.Trim())) {
						nonterminalsEpsilon.Add(rule.LHS.Name.Trim());
						continue;
					}

					bool isEmpty = true;
					foreach (Nonterminal nonterm in rule.RHS) {
						if (!nonterminalsEpsilon.Contains(nonterm.Name.Trim())) {
							isEmpty = false;
							break;
						}
					}
					if (!isEmpty) {
						continue;
					} else if (!nonterminalsEpsilon.Contains(rule.LHS.Name.Trim())) {
						nonterminalsEpsilon.Add(rule.LHS.Name.Trim());
						continue;
					}
				}
			}

			string[] rowIndexes = new string[symbols.GetLength(0)];
			for (int i = 0; i < symbols.GetLength(0); i++) {
				rowIndexes[i] = symbols[i, 0];
			}

			string[] colIndexes = new string[symbols.GetLength(1)];
			for (int i = 0; i < symbols.GetLength(1); i++) {
				colIndexes[i] = symbols[0, i];
			}

			foreach (Rule rule in g.Rules) {
				string nsym = rule.LHS.Name.Trim();
				
				if (rule.RHS.Count == 0) {
					symbols[Array.IndexOf(rowIndexes, nsym), Array.IndexOf(colIndexes, nsym)] = "*";
					continue;
				}
				
				foreach (Symbol symbol in rule.RHS) {
					string sym = symbol.Name.Trim();
					if (nonterminalsEpsilon.Contains(sym)) {
						symbols[Array.IndexOf(rowIndexes, nsym), Array.IndexOf(colIndexes, sym)] = "*";
						continue;
					}

					if (sym.Equals(sym.ToLower())) {
						symbols[Array.IndexOf(rowIndexes, nsym), Array.IndexOf(colIndexes, sym)] = "*";
						break;
					}					
				}
			}

			bool brokeOut = false;
			while (true) {
				bool isChanged = false;
				for (int i = 1; i < rows; i++) {
					for (int j = 1; j < rows; j++) {
						string str = symbols[i, j];
						if (str == null) {
							continue;
						}
						
						if (str == "*") {
							isChanged = CopyLine(symbols, i, j) || isChanged;
						}
					}

					if (i == 1 && !isChanged) {
						brokeOut = true;
						break;
					}
				}

				if (brokeOut) {
					break;
				}
			}

			Console.WriteLine();
			for (int i = 0; i < rows; i++) {
				for (int j = 0; j < cols; j++) {
					string str = symbols[i, j];
					if (str == null) {
						str = " ";
					}
					Console.Write(str + " ");
				}

				Console.WriteLine();
			}

			Console.WriteLine();
			foreach (Rule rule in g.Rules) {
				string res = "first[" + rule.LHS.Name.Trim() + ":";

				if (rule.RHS.Count == 0) {
					res += "{e}] = {e}";
					Console.WriteLine(res);
					continue;
				}

				foreach (Symbol sym in rule.RHS) {
					res += sym.Name.Trim();
				}

				res += "] = ";
				string subres = "";

				foreach (Symbol sym in rule.RHS) {
					string symbol = sym.Name.Trim();

					if (symbol.Equals(symbol.ToLower())) {
						subres += symbol;
						break;
					}

					if (symbol.Equals(symbol.ToUpper())) {
						int index = Array.IndexOf(rowIndexes, symbol);
						for (int i = rows; i < cols; i++) {
							string included = symbols[index, i];
							if (!(included == null) && included.Equals("*")) {
								if (!subres.Contains(symbols[0, i])) {
									subres += symbols[0, i] + " ";
								} else if (nonterminalsEpsilon.Contains(symbol)) {
									subres += "{e}";
								}
							}
						}

						if (!nonterminalsEpsilon.Contains(symbol)) {
							break;
						}
					}
				}

				res += subres;

				Console.WriteLine(res);
			}

			cols++;
			symbols = new string[rows, cols];
			
			for (int i = 1; i < rows; i++) {
				symbols[i, 0] = nonterminals[i - 1];
			}

			for (int i = 1; i < rows; i++) {
				symbols[0, i] = nonterminals[i - 1];
			}

			for (int i = rows; i < cols - 1; i++) {
				symbols[0, i] = terminals[i - rows];
			}

			symbols[0, cols - 1] = "e";
			symbols[Array.IndexOf(rowIndexes, g.StartingNonterminal.Name.Trim()), cols - 1] = "*";
		}

		private bool CopyLine(string[,] symbols, int row, int col) {
			bool res = false;
			for (int i = 1; i < symbols.GetLength(1); i++) {
				string str = symbols[col, i];
				if (str == null) {
					continue;
				}

				if (str == "*") {
					if ((symbols[row, i] == null) ||
						(!(symbols[row, i] == null) && !symbols[row, i].Equals("*"))) {
						res = true;
					}
					symbols[row, i] = "*";
				}
			}

			return res;
		}

		private IGrammar g;
	}
}
