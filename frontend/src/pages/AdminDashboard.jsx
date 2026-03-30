import { useState } from "react";

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

export default function AdminDashboard(){

  const [selectedUser,setSelectedUser]=useState(null);
  const [selectedSession,setSelectedSession]=useState(null);

  return(

    <div className="min-h-screen bg-black text-white p-6">

      <h1 className="text-3xl font-bold mb-6">
        PHEMA Admin Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        <SystemStatus/>
        <LiveFeed/>

      </div>

      <div className="mt-6">
        <AdminStats/>
      </div>

      <div className="mt-6">
        <AdminCampaignPanel/>
      </div>

      <div className="mt-6">

        <AdminUserList
          onSelectUser={(u)=>{

            setSelectedUser(u);
            setSelectedSession(null);

          }}
        />

      </div>

      {selectedUser&&(

        <div className="mt-6">

          <AdminSessionList
            userId={selectedUser}
            onSelectSession={setSelectedSession}
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