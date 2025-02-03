{
  pkgs,
  lib,
  config,
  inputs,
  ...
}: {
  packages = [
    pkgs.git
    pkgs.alejandra
  ];

  dotenv.enable = true;

  languages = {
    python = {
      enable = true;
      package = pkgs.python312;

      venv.enable = true;

      uv = {
        enable = true;
        sync.enable = true;
      };
    };
  };

  scripts.run-server.exec = ''
    python bada.py
  '';
}
