import { useState,useEffect } from "react";

import UserIdentityPanel from "../components/user/UserIdentityPanel";
import UserScanPanel from "../components/user/UserScanPanel";
import UserSessionHistory from "../components/user/UserSessionHistory";
import UserResultPanel from "../components/user/UserResultPanel";
import UserAdvicePanel from "../components/user/UserAdvicePanel";
import UserSessionSummary from "../components/user/UserSessionSummary";

export default function UserDashboard(){

  const [identity,setIdentity]=useState(null);

  const [selectedSession,setSelectedSession]=useState(null);

  const storedUserId=
    localStorage.getItem("user_id");

  useEffect(()=>{

    if(!storedUserId){

      window.location="/login";

    }

  },[]);

  return(

    <div className="min-h-screen bg-black text-white p-6">

      <h1 className="text-3xl font-bold mb-6">

        PHEMA User Portal

      </h1>

      <UserIdentityPanel

        fixedUserId={storedUserId}

        onSessionReady={setIdentity}

      />

      {identity && (

        <>

          <UserScanPanel

            userId={storedUserId}

            sessionId={identity.sessionId}

          />

          <UserSessionHistory

            userId={storedUserId}

            onSelectSession={

              setSelectedSession

            }

          />

          {selectedSession && (

            <>

              <UserResultPanel

                userId={storedUserId}

                sessionId={selectedSession}

                entityId={selectedSession}

                entityType="session"

              />

              <UserSessionSummary

                userId={storedUserId}

                sessionId={selectedSession}

              />

              <UserAdvicePanel

                userId={storedUserId}

                sessionId={selectedSession}

              />

            </>

          )}

        </>

      )}

    </div>

  );

}