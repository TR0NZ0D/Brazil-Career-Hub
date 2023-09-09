export function cutText(text: string, maxLenght: number): string {
  if (text.length > maxLenght) {
    text = text.slice(0, maxLenght);
    text += "...";
  }

  return text;
}