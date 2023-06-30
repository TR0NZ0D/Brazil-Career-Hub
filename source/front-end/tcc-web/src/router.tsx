import { createBrowserRouter } from 'react-router-dom';
import Signup from './views/Signup/Signup';
import Home from './views/Home/Home';

const router = createBrowserRouter([
  {
    path: "signup",
    element: <Signup />
  },
  {
    path: "/",
    element: <Home />
  }
])

export default router;