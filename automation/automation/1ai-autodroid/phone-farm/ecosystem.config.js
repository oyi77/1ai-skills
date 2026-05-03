module.exports = {
  apps: [
    {
      name: 'phonefarm',
      script: '/usr/bin/python3',
      args: 'farm_daemon.py --mode dashboard --port 8889',
      cwd: '/mnt/data/berkahkarya/skills/1ai-skills/automation/1ai-autodroid/phone-farm',
      interpreter: 'none',
      env: {
        PYTHONUNBUFFERED: '1',
      },
      restart_delay: 5000,
      max_restarts: 10,
      autorestart: true,
      watch: false,
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      error_file: '/home/openclaw/.pm2/logs/phonefarm-error.log',
      out_file: '/home/openclaw/.pm2/logs/phonefarm-out.log',
    },
  ],
};
