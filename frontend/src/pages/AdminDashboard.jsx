import { useState,useEffect } from "react";
import { useNavigate } from "react-router-dom";

import SystemStatus from "../components/admin/SystemStatus";
import LiveFeed from "../components/admin/LiveFeed";
import EntityInvestigation from "../components/admin/EntityInvestigation";
import AttackTimeline from "../components/admin/AttackTimeline";
import AttackGraph from "../components/admin/AttackGraph";
import AdminStats from "../components/admin/AdminStats";
import AdminCampaignPanel from "../components/admin/AdminCampaignPanel";
import AdminEventViewer from "../components/admin/AdminEventViewer";

import AdminUserList from "../components/admin/AdminUserList";
import AdminSessionList from "../components/admin/AdminSessionList";
import AdminAlertsPanel from "../components/admin/AdminAlertsPanel";
import LogoutButton from "../components/common/LogoutButton";

export default function AdminDashboard(){

  const navigate=useNavigate();

  const [selectedUser,setSelectedUser]=useState(null);
  const [selectedSession,setSelectedSession]=useState(null);

  /* AUTH VALIDATION */

  useEffect(()=>{

    const token=
      localStorage.getItem("token");

    const role=
      localStorage.getItem("role");

    if(!token || role!=="admin"){

      navigate("/login");

    }

  },[navigate]);

  /* RESTORE STATE AFTER REFRESH */

  useEffect(()=>{

    const savedUser=
      localStorage.getItem("admin_selected_user");

    const savedSession=
      localStorage.getItem("admin_selected_session");

    if(savedUser){

      setSelectedUser(savedUser);

    }

    if(savedSession){

      setSelectedSession(savedSession);

    }

  },[]);

  /* SAVE USER SELECTION */

  const handleUserSelect=(u)=>{

    setSelectedUser(u);
    setSelectedSession(null);

    localStorage.setItem(
      "admin_selected_user",
      u
    );

    localStorage.removeItem(
      "admin_selected_session"
    );

  };

  /* SAVE SESSION SELECTION */

  const handleSessionSelect=(s)=>{

    setSelectedSession(s);

    localStorage.setItem(
      "admin_selected_session",
      s
    );

  };

  return(

    <div className="min-h-screen bg-black text-white p-6">

      <h1 className="text-3xl font-bold mb-6">
        PHEMA Admin Dashboard
      </h1>

      <div className="flex justify-end mb-6">
        <LogoutButton/>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        <SystemStatus/>
        <LiveFeed/>
        <AdminAlertsPanel/>
      </div>
      

      <div className="mt-6">
        <AdminStats/>
      </div>

      <div className="mt-6">
        <AdminCampaignPanel/>
      </div>

      <div className="mt-6">

        <AdminUserList
          onSelectUser={handleUserSelect}
        />

      </div>

      {selectedUser&&(

        <div className="mt-6">

          <AdminSessionList
            userId={selectedUser}
            onSelectSession={handleSessionSelect}
          />

        </div>

      )}

      {selectedUser&&selectedSession&&(

        <>

          <div className="mt-6">

            <EntityInvestigation
              userId={selectedUser}
              sessionId={selectedSession}
            />

          </div>

          <div className="mt-6">

            <AttackTimeline
              userId={selectedUser}
              sessionId={selectedSession}
            />

          </div>

          <div className="mt-6">

            <AdminEventViewer
              userId={selectedUser}
              sessionId={selectedSession}
            />

          </div>

          <div className="mt-6">

            <AttackGraph
              userId={selectedUser}
              sessionId={selectedSession}
            />

          </div>

        </>

      )}

    </div>

  );

}