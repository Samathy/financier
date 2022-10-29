# Fiancier

Convert csv exports from banks into a consistent format for 
importing into accounting systems.

## Output Format
A CSV with the following columns:
* `date` - dd/mm/yyy
* description - The payment description.
* in - Money in, as a decimal
* out - Money out, as a decimal
* balance - the balance after the transaction took place

## Supported input formats
See `financier/formats/`

* Monzo
* Barclays Debit
* LLoyds Debit
* Nationwide Debit
* Nationwide Credit Card

### Notes
Some banks export a CSV containing all the data required, and this script just shifts it about into the right columns.
Some banks have export formats requiring calculations to be performed
in order to get the output we want.
Some banks provide transactions in reverse order.
The point is, that this script has various methods for performing pre-processing on input,
specific calculations on the input, and post-processing on the input.
If you wish to write a format yourself, please do ask for a guide on how to do
it. This script is extensible enough that it should be 
relatively easy to specify the operations needed, but since anyone else using
this is unlikely, I havent documented how that works yet. Sorry.
