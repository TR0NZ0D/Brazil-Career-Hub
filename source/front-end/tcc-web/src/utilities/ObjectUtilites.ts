export function setNullIfPropertiesAreEmpty(obj: any): any | null {
  if (Object.values(obj).every(x => x === undefined || x === '' || x === null)) {
    return null;
  }

  return obj;
}