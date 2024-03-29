import { createBrowserRouter } from 'react-router-dom';
import Signup from './views/Signup/Signup';
import Home from './views/Home/Home';
import Login from 'views/Login/ProjectLogin';
import MyResumes from 'views/MyResumes/MyResumes';

const router = createBrowserRouter([
  {
    path: "signup",
    element: <Signup />
  },
  {
    path: "login",
    element: <Login />
  },
  {
    path: "/",
    element: <Home />
  },
  {
    path: "/myresumes",
    element: <MyResumes />
  }
])

export default router;