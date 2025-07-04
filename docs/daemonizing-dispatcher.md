# Running the Dispatcher as a Daemon

This guide explains how to keep `scripts/dispatch.sh` running continuously in a
dockerized environment on both Linux (systemd) and macOS (launchd).

## Linux: systemd Service

Create `/etc/systemd/system/view-factory.service` with the following content:

```ini
[Unit]
Description=SwiftUI View Factory Dispatcher
After=network.target docker.service
Requires=docker.service

[Service]
WorkingDirectory=/path/to/SwiftUI-View-Factory
ExecStart=/path/to/SwiftUI-View-Factory/scripts/docker_dispatch.sh
Restart=always
Environment=OPENAI_API_KEY=…

[Install]
WantedBy=multi-user.target
```

Then reload and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now view-factory.service
```

The dispatcher will now restart automatically on failure while running inside
`python:3.11-slim` (or a custom `DOCKER_IMAGE`).

## macOS: launchd Agent

Create `~/Library/LaunchAgents/com.example.viewfactory.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.example.viewfactory</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/docker</string>
        <string>run</string>
        <string>--rm</string>
        <string>-v</string><string>/path/to/SwiftUI-View-Factory:/repo</string>
        <string>-w</string><string>/repo</string>
        <string>python:3.11-slim</string>
        <string>bash</string>
        <string>scripts/dispatch.sh</string>
    </array>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
    <key>EnvironmentVariables</key>
    <dict>
        <key>OPENAI_API_KEY</key><string>…</string>
    </dict>
</dict>
</plist>
```

Load the agent with:

```bash
launchctl load ~/Library/LaunchAgents/com.example.viewfactory.plist
```

The dispatcher will run in Docker and relaunch automatically when the Mac
boots.
