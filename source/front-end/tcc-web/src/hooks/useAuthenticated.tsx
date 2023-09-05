import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function useAuthenticated(): void {

  const navigate = useNavigate();

  useEffect(() => {
    const entityStored = localStorage.getItem('entity-logged');
    if (entityStored === null)
      navigate("/login");
  })
}

export default useAuthenticated;
