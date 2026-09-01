export interface HealthResponse {
  status: 'healthy' | 'degraded' | 'error';
  project: string;
  version: string;
  environment: string;
  timestamp: string;
  services: {
    database: {
      status: string;
      database_url?: string;
      error?: string;
    };
    llm_provider: {
      provider: string;
      model: string;
      configured: boolean;
    };
    vector_store: {
      backend: string;
      collection: string;
    };
    storage: {
      backend: string;
      directory: string;
    };
  };
}
