import React, { useState } from 'react';
import { Users, UserPlus, Shield, X, Check, Building, Mail } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleButton } from '../apple/AppleButton';
import { AppleBadge } from '../apple/AppleBadge';
import { RoleBadge } from '../apple/RoleBadge';
import { useCurrentTenant, useTeamMembers, useInviteMember, useUpdateUserRole, UserRole } from '../../api/tenants';

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export const TeamManagementModal: React.FC<Props> = ({ isOpen, onClose }) => {
  const { data: tenant } = useCurrentTenant();
  const { data: members, isLoading } = useTeamMembers();
  const inviteMember = useInviteMember();
  const updateRole = useUpdateUserRole();

  const [inviteEmail, setInviteEmail] = useState('');
  const [inviteName, setInviteName] = useState('');
  const [inviteRole, setInviteRole] = useState<UserRole>('sales');
  const [isInviteOpen, setIsInviteOpen] = useState(false);

  if (!isOpen) return null;

  const handleInvite = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inviteEmail || !inviteName) return;
    inviteMember.mutate(
      { email: inviteEmail, full_name: inviteName, role: inviteRole },
      {
        onSuccess: () => {
          setInviteEmail('');
          setInviteName('');
          setIsInviteOpen(false);
        },
      }
    );
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs" onClick={onClose} />
      <div className="relative w-full max-w-2xl bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden z-50 flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-6 border-b border-slate-100 flex items-center justify-between bg-gradient-to-r from-slate-900 to-indigo-950 text-white">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-2xl bg-white/10 border border-white/10">
              <Users size={20} />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-lg font-bold tracking-tight">{tenant?.name || "Butler's Leather"}</h3>
                <span className="px-2 py-0.5 rounded-full bg-white/20 text-white text-[10px] font-bold uppercase font-mono">
                  {tenant?.plan || 'Enterprise'} Plan
                </span>
              </div>
              <p className="text-xs text-slate-300 font-medium">Organisation & Role-Based Access Control (RBAC)</p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 cursor-pointer"
          >
            <X size={18} />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 overflow-y-auto space-y-5 flex-1">
          {/* Action Bar */}
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Authorized Team Members ({members?.length || 4})
            </h4>
            <AppleButton
              variant="primary"
              size="sm"
              icon={<UserPlus size={14} />}
              onClick={() => setIsInviteOpen(!isInviteOpen)}
            >
              {isInviteOpen ? 'Cancel' : 'Invite Member'}
            </AppleButton>
          </div>

          {/* Invite Member Form Drawer */}
          {isInviteOpen && (
            <form onSubmit={handleInvite} className="p-4 rounded-2xl bg-blue-50/60 border border-blue-200 space-y-3">
              <h5 className="text-xs font-bold text-blue-950">Provision New Team Member</h5>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                <input
                  type="text"
                  placeholder="Full Name"
                  value={inviteName}
                  onChange={(e) => setInviteName(e.target.value)}
                  className="px-3 py-2 text-xs rounded-xl bg-white border border-slate-300 font-medium outline-none focus:border-blue-500"
                  required
                />
                <input
                  type="email"
                  placeholder="name@company.in"
                  value={inviteEmail}
                  onChange={(e) => setInviteEmail(e.target.value)}
                  className="px-3 py-2 text-xs rounded-xl bg-white border border-slate-300 font-medium outline-none focus:border-blue-500"
                  required
                />
                <select
                  value={inviteRole}
                  onChange={(e) => setInviteRole(e.target.value as UserRole)}
                  className="px-3 py-2 text-xs rounded-xl bg-white border border-slate-300 font-bold text-slate-800 outline-none"
                >
                  <option value="sales">Export Sales</option>
                  <option value="compliance">Compliance & EUDR</option>
                  <option value="finance">Finance & Banking</option>
                  <option value="auditor">Auditor (Read-Only)</option>
                  <option value="owner">Owner / Co-Founder</option>
                </select>
              </div>
              <div className="flex justify-end">
                <AppleButton variant="primary" size="sm" type="submit">
                  Send Access Invite
                </AppleButton>
              </div>
            </form>
          )}

          {/* Members List */}
          <div className="space-y-2.5">
            {members?.map((user) => (
              <div
                key={user.id}
                className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-3.5 rounded-2xl bg-slate-50 border border-slate-200/90 gap-3"
              >
                <div className="space-y-0.5">
                  <div className="flex items-center gap-2">
                    <h5 className="text-sm font-bold text-slate-900">{user.full_name}</h5>
                    <RoleBadge role={user.role} />
                  </div>
                  <p className="text-xs text-slate-500 font-mono flex items-center gap-1.5">
                    <Mail size={12} className="text-slate-400" /> {user.email}
                  </p>
                </div>

                {/* Role Switcher */}
                <div className="flex items-center gap-2 shrink-0">
                  <select
                    value={user.role}
                    onChange={(e) => updateRole.mutate({ userId: user.id, role: e.target.value as UserRole })}
                    className="text-xs font-semibold px-2.5 py-1 rounded-xl bg-white border border-slate-300 text-slate-700 outline-none cursor-pointer hover:border-slate-400"
                  >
                    <option value="owner">Owner & MD</option>
                    <option value="sales">Export Sales</option>
                    <option value="compliance">Compliance & EUDR</option>
                    <option value="finance">Finance & Banking</option>
                    <option value="auditor">Auditor</option>
                  </select>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 px-6 border-t border-slate-100 bg-slate-50 flex items-center justify-between text-xs text-slate-500">
          <span>Enterprise Tenant ID: <b className="font-mono text-slate-700">{tenant?.id.substring(0, 8)}...</b></span>
          <AppleButton variant="secondary" size="sm" onClick={onClose}>
            Done
          </AppleButton>
        </div>
      </div>
    </div>
  );
};
