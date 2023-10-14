import { useEffect } from 'react';

function useNeverEmptyArray<T>(items: T[], setItems: (items: T[]) => void) {
  useEffect(() => {
    if (items.length === 0) {
      setItems([{} as T]);
    }
  }, [items]);
}

export default useNeverEmptyArray;
