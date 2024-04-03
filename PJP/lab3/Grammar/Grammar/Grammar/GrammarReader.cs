using System;
using System.IO;
namespace Grammar
{
	public sealed class GrammarReader
	{
		public GrammarReader(StreamReader input)
		{
			inp = input;
		}

		public IGrammar Read()
		{
			GrammarImpl grammar = new GrammarImpl();

			ch = inp.Read();
			int sym = GetSymbol();

			while( sym != -1 ) 
			{
				if( sym != SYM_NT )
					error("Na leve strane pravidla se ocekava nonterminal");
				Nonterminal lhs = grammar.AddNonterminal(attr.ToString());
				if( grammar.StartingNonterminal == null )
					grammar.StartingNonterminal = lhs;
				sym = GetSymbol();
				if( sym != ':' )
					error("Ocekava se dvojtecka");
				do 
				{
					sym = GetSymbol();
					Rule rule = new Rule(lhs);

					while( sym == SYM_NT || sym == SYM_T ) 
					{
						Symbol symbol = (sym == SYM_NT)? grammar.AddNonterminal(attr) : grammar.AddTerminal(attr);
						rule.RHS.Add(symbol);
						sym = GetSymbol();

					}
					lhs.AddRule(rule);
				} while( sym == '|' );
				if( sym != ';' )
					error("Ocekava se strednik");
				sym = GetSymbol();
			}
			return grammar;
		}

		private void error(string msg)
		{
			throw new GrammarException(msg, lineNumber);
		}

		private const int SYM_NT  = 'N';
		private const int SYM_T   = 'T';
		private const int SYM_EOF = -1;

		private int GetSymbol()
		{
			for(;;) 
			{
				if( ch == '\n' ) lineNumber++;
				if( ch < 0 )
					return SYM_EOF;
				if( Char.IsWhiteSpace((char)ch) )
					ch = inp.Read();
				else if( ch == '{' ) 
				{
					do 
					{
						ch = inp.Read();
						if (ch == '\n') lineNumber++;
					} while( ch >= 0 && ch != '}' );
					if( ch >= 0 )
						ch = inp.Read();
				} 
				else
					break;
			}

			if( Char.IsLetter((char)ch) ) 
			{
				String buf = " "; ////new String();
				do 
				{
					buf +=((char)ch);
					ch = inp.Read();
					if( ch == '\n' ) lineNumber++;
				} while( ch > 0 && Char.IsLetterOrDigit((char)ch) );
				attr = buf.ToString();
				return Char.IsLower(attr[0]) ? SYM_T : SYM_NT;
			}

			int sym = ch;
			ch = inp.Read();
			if( ch == '\n' ) lineNumber++;
			return sym;
		}

		private StreamReader inp;
		private int ch;
		private string attr= "";
		private int lineNumber = 1;
	}
}