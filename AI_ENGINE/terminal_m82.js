const express = require('express');
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: 'postgresql://neondb_owner:npg_ITKjtbnJ9Xe6@ep-cold-thunder-am83t90o-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require',
  ssl: { rejectUnauthorized: false },
});
