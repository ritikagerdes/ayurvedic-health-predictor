import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';

export const LoginButton: React.FC = () => {
  const { loginWithRedirect } = useAuth0();

  return (
    <button
      onClick={() => loginWithRedirect()}
      className="bg-emerald-600 text-white font-bold py-3 px-8 rounded-lg shadow-lg hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 transition-colors duration-300"
    >
      Log In / Sign Up
    </button>
  );
};

export const LogoutButton: React.FC = () => {
  const { logout } = useAuth0();

  return (
    <button
      onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}
      className="text-slate-600 hover:text-slate-800 font-medium py-2 px-4 rounded-lg hover:bg-slate-100 transition-colors duration-200"
    >
      Log Out
    </button>
  );
};

export const UserProfile: React.FC = () => {
  const { user, isAuthenticated } = useAuth0();

  if (!isAuthenticated || !user) {
    return null;
  }

  return (
    <div className="flex items-center space-x-3">
      {user.picture && (
        <img
          src={user.picture}
          alt={user.name}
          className="h-10 w-10 rounded-full border-2 border-emerald-600"
        />
      )}
      <div>
        <p className="text-sm font-medium text-slate-800">{user.name}</p>
        <p className="text-xs text-slate-500">{user.email}</p>
      </div>
    </div>
  );
};