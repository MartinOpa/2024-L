using System;
namespace Grammar
{
	public class GrammarException : Exception
	{
		public GrammarException(string msg, int lineNumber) : base(msg)
		{
			this.LineNumber = lineNumber;
		}
		public int LineNumber { get; }
	}
}