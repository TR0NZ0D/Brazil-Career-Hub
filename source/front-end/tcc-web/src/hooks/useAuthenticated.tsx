import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function useAuthenticated(type: "company" | "user" | "any"): void {
  const navigate = useNavigate();

  useEffect(() => {
    const entityOnStorage = localStorage.getItem("entity-logged");
    if (entityOnStorage !== null) {
      const entity = JSON.parse(entityOnStorage);

      if (entity.cnpj === undefined && type === "company")
        navigate("/");
      else if (entity.cnpj !== undefined && type === "user")
        navigate("/");
    }
    else {
      navigate("/login");
    }
  }, [])
}

export default useAuthenticated;
