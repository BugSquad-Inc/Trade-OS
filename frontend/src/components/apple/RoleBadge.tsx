import React from 'react';
import { Shield, Award, DollarSign, FileCheck, Eye } from 'lucide-react';
import { AppleBadge } from './AppleBadge';
import { UserRole } from '../../api/tenants';

interface RoleBadgeProps {
  role: UserRole;
  size?: 'sm' | 'md';
}

export const RoleBadge: React.FC<RoleBadgeProps> = ({ role, size = 'sm' }) => {
  const configs: Record<UserRole, { tone: 'purple' | 'blue' | 'green' | 'orange' | 'zinc'; label: string; icon: React.ReactNode }> = {
    owner: { tone: 'purple', label: 'Owner & MD', icon: <Award size={12} /> },
    sales: { tone: 'blue', label: 'Export Sales', icon: <DollarSign size={12} /> },
    compliance: { tone: 'green', label: 'Compliance & EUDR', icon: <FileCheck size={12} /> },
    finance: { tone: 'orange', label: 'Finance & Banking', icon: <Shield size={12} /> },
    auditor: { tone: 'zinc', label: 'Auditor (Read-Only)', icon: <Eye size={12} /> },
  };

  const config = configs[role] || configs.sales;

  return (
    <AppleBadge tone={config.tone} size={size} icon={config.icon}>
      {config.label}
    </AppleBadge>
  );
};
