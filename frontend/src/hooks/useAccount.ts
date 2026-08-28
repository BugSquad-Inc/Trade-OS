import { useQuery } from '@tanstack/react-query';
import { getAccount360 } from '../api/accounts';

export function useAccount(id: string | null) {
  return useQuery({
    queryKey: ['account', id],
    queryFn: () => (id ? getAccount360(id) : null),
    enabled: !!id,
  });
}
