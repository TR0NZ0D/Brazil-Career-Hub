import { createContext, useState } from 'react';
import { ProviderProps } from './ProviderProps';

type UIContextProps = {
  loading: boolean;
  setLoading: (val: boolean) => void;
}

export const UIContext = createContext({} as UIContextProps);

export const UIContextProvider = ({ children }: ProviderProps) => {
  const [loading, setLoading] = useState<boolean>(false);

  return (
    <UIContext.Provider value={{
      loading,
      setLoading
    }}>
      {children}
    </UIContext.Provider>
  )
}