export default () => ({
  port: Number(process.env.PORT) | 3001,
  database: {
    host: process.env.DB_HOST,
    port: Number(process.env.DB_PORT) || 5432,
    username: process.env.DB_USERNAME,
    password: process.env.DB_PASSWORD,
    name: process.env.DB_NAME,
  },
});
