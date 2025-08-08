docker run `
   --mount type=bind,src="$PSScriptRoot",dst=/scenarioFolder `
   landis_ii_v7_linux /bin/sh -c "cd /scenarioFolder && dotnet `$LANDIS_CONSOLE SimEffectEC.txt"

pause
