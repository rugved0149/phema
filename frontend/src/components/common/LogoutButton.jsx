import { api } from "../../api/client";

export default function LogoutButton(){

  const handleLogout=async()=>{

    try{

      await api.post(
        "/auth/logout"
      );

    }catch(e){

      console.error(e);

    }

    localStorage.clear();

    window.location="/login";

  };

  return(

    <button
      onClick={handleLogout}
      className="bg-red-600 px-3 py-2 rounded"
    >
      Logout
    </button>

  );

}