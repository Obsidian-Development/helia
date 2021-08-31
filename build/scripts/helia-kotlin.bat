@rem
@rem Copyright 2015 the original author or authors.
@rem
@rem Licensed under the Apache License, Version 2.0 (the "License");
@rem you may not use this file except in compliance with the License.
@rem You may obtain a copy of the License at
@rem
@rem      https://www.apache.org/licenses/LICENSE-2.0
@rem
@rem Unless required by applicable law or agreed to in writing, software
@rem distributed under the License is distributed on an "AS IS" BASIS,
@rem WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@rem See the License for the specific language governing permissions and
@rem limitations under the License.
@rem

@if "%DEBUG%" == "" @echo off
@rem ##########################################################################
@rem
@rem  helia-kotlin startup script for Windows
@rem
@rem ##########################################################################

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%..

@rem Resolve any "." and ".." in APP_HOME to make it shorter.
for %%i in ("%APP_HOME%") do set APP_HOME=%%~fi

@rem Add default JVM options here. You can also use JAVA_OPTS and HELIA_KOTLIN_OPTS to pass JVM options to this script.
set DEFAULT_JVM_OPTS=

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if "%ERRORLEVEL%" == "0" goto execute

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto execute

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:execute
@rem Setup the command line

set CLASSPATH=%APP_HOME%\lib\helia-kotlin-1.0-SNAPSHOT.jar;%APP_HOME%\lib\kord-extensions-1.4.4-RC3.jar;%APP_HOME%\lib\annotations-1.4.4-RC3.jar;%APP_HOME%\lib\koin-logger-slf4j-3.0.2.jar;%APP_HOME%\lib\kord-core-0.8.0-M4.jar;%APP_HOME%\lib\token-parser-1.4.4-RC3.jar;%APP_HOME%\lib\kord-rest-0.8.0-M4.jar;%APP_HOME%\lib\kord-gateway-0.8.0-M4.jar;%APP_HOME%\lib\kord-common-0.8.0-M4.jar;%APP_HOME%\lib\cache-map-0.3.0.jar;%APP_HOME%\lib\cache-api-0.3.0.jar;%APP_HOME%\lib\kotlin-logging-jvm-2.0.10.jar;%APP_HOME%\lib\koin-core-jvm-3.0.2.jar;%APP_HOME%\lib\ktor-client-serialization-jvm-1.6.0.jar;%APP_HOME%\lib\ktor-client-json-jvm-1.6.0.jar;%APP_HOME%\lib\ktor-client-cio-jvm-1.6.0.jar;%APP_HOME%\lib\ktor-client-websockets-jvm-1.6.0.jar;%APP_HOME%\lib\ktor-client-core-jvm-1.6.0.jar;%APP_HOME%\lib\ktor-http-cio-jvm-1.6.0.jar;%APP_HOME%\lib\ktor-network-tls-jvm-1.6.0.jar;%APP_HOME%\lib\ktor-http-jvm-1.6.0.jar;%APP_HOME%\lib\ktor-network-jvm-1.6.0.jar;%APP_HOME%\lib\ktor-utils-jvm-1.6.0.jar;%APP_HOME%\lib\ktor-io-jvm-1.6.0.jar;%APP_HOME%\lib\kotlinx-coroutines-core-jvm-1.5.0.jar;%APP_HOME%\lib\kotlin-stdlib-jdk8-1.5.21.jar;%APP_HOME%\lib\groovy-3.0.8.jar;%APP_HOME%\lib\logback-classic-1.2.5.jar;%APP_HOME%\lib\commons-text-1.9.jar;%APP_HOME%\lib\commons-validator-1.7.jar;%APP_HOME%\lib\icu4j-69.1.jar;%APP_HOME%\lib\kotlinx-serialization-json-jvm-1.2.1.jar;%APP_HOME%\lib\sentry-5.0.0.jar;%APP_HOME%\lib\atomicfu-jvm-0.16.1.jar;%APP_HOME%\lib\kotlinx-serialization-core-jvm-1.2.1.jar;%APP_HOME%\lib\kotlin-stdlib-jdk7-1.5.21.jar;%APP_HOME%\lib\kotlinx-datetime-jvm-0.2.1.jar;%APP_HOME%\lib\kotlin-stdlib-1.5.21.jar;%APP_HOME%\lib\logback-core-1.2.5.jar;%APP_HOME%\lib\slf4j-api-1.7.31.jar;%APP_HOME%\lib\commons-lang3-3.11.jar;%APP_HOME%\lib\commons-beanutils-1.9.4.jar;%APP_HOME%\lib\commons-digester-2.1.jar;%APP_HOME%\lib\commons-logging-1.2.jar;%APP_HOME%\lib\commons-collections-3.2.2.jar;%APP_HOME%\lib\gson-2.8.5.jar;%APP_HOME%\lib\annotations-13.0.jar;%APP_HOME%\lib\kotlin-stdlib-common-1.5.21.jar


@rem Execute helia-kotlin
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %HELIA_KOTLIN_OPTS%  -classpath "%CLASSPATH%" helia.AppKt %*

:end
@rem End local scope for the variables with windows NT shell
if "%ERRORLEVEL%"=="0" goto mainEnd

:fail
rem Set variable HELIA_KOTLIN_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd.exe /c_ return code!
if  not "" == "%HELIA_KOTLIN_EXIT_CONSOLE%" exit 1
exit /b 1

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
