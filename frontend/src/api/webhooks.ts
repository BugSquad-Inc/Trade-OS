import { fetchApi } from './client';

export interface WebhookSubscriptionItem {
  id: string;
  target_url: string;
  events: string[];
  is_active: boolean;
  created_at: string;
}

export interface WebhookListResponse {
  total_count: number;
  subscriptions: WebhookSubscriptionItem[];
}

export const listWebhooksApi = () => fetchApi<WebhookListResponse>('/api/v1/webhooks');
export const subscribeWebhookApi = (target_url: string, events: string[]) =>
  fetchApi<WebhookSubscriptionItem>('/api/v1/webhooks/subscribe', {
    method: 'POST',
    body: JSON.stringify({ target_url, events }),
  });
