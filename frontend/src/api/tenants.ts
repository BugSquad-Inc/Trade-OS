import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchApi } from './client';

export type UserRole = 'owner' | 'sales' | 'compliance' | 'finance' | 'auditor';

export interface UserAccount {
  id: string;
  tenant_id: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  oidc_sub?: string;
  last_login_at?: string;
  created_at: string;
}

export interface Tenant {
  id: string;
  name: string;
  slug: string;
  country_code: string;
  plan: string;
  status: string;
  settings: Record<string, any>;
  users: UserAccount[];
  created_at: string;
  updated_at: string;
}

export function useCurrentTenant() {
  return useQuery<Tenant>({
    queryKey: ['current_tenant'],
    queryFn: () => fetchApi<Tenant>('/api/v1/tenants/current'),
  });
}

export function useTeamMembers() {
  return useQuery<UserAccount[]>({
    queryKey: ['team_members'],
    queryFn: () => fetchApi<UserAccount[]>('/api/v1/tenants/members'),
  });
}

export function useCurrentUser() {
  return useQuery<UserAccount>({
    queryKey: ['current_user'],
    queryFn: () => fetchApi<UserAccount>('/api/v1/users/me'),
  });
}

export function useInviteMember() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: { email: string; full_name: string; role: UserRole }) =>
      fetchApi<UserAccount>('/api/v1/tenants/members/invite', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['team_members'] });
      queryClient.invalidateQueries({ queryKey: ['current_tenant'] });
    },
  });
}

export function useUpdateUserRole() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ userId, role }: { userId: string; role: UserRole }) =>
      fetchApi<UserAccount>(`/api/v1/tenants/members/${userId}/role`, {
        method: 'PATCH',
        body: JSON.stringify({ role }),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['team_members'] });
      queryClient.invalidateQueries({ queryKey: ['current_tenant'] });
    },
  });
}
