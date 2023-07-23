export function appendZeroToNumber(number: string | number): string {
  if (typeof number === "number")
    return appendZeroToNumber(number.toString());

  else if (number.length === 1)
    return "0" + number;

  return number;
}
