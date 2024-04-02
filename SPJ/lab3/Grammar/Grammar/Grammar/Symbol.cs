using System;

namespace Grammar
{
    public abstract class Symbol : IComparable<Symbol>
	{
		protected Symbol(string name)
		{
			this.Name = name;
		}

		public string Name { get; }

		public int CompareTo(Symbol? other)
		{
			if (other is null) throw new ArgumentNullException(nameof(other), " cannot be null");
			return Name.CompareTo(other.Name);
		}
	}
}