{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
    buildInputs = [
        pkgs.python3
        pkgs.python3Packages.ollama
        pkgs.python3Packages.flask-socketio
        pkgs.python3Packages.flask
    ];
}