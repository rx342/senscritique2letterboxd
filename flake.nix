{
  description = "senscritique2letterboxd flake";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs =
    {
      nixpkgs,
      poetry2nix,
      ...
    }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      poetryEnv = (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }).mkPoetryEnv {
        projectDir = ./.;
        preferWheels = true;
      };
      poetryApp = (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }).mkPoetryApplication {
        projectDir = ./.;
        preferWheels = true;
      };
      formatter = pkgs.nixfmt-rfc-style;
    in
    {
      devShells.${system} = rec {
        dev = pkgs.mkShell {
          nativeBuildInputs = [
            pkgs.poetry
            poetryEnv
            formatter
          ];
        };
        default = dev;
      };

      packages.${system} = rec {
        s2l = poetryApp;
        default = s2l;
      };

      apps.${system} = rec {
        s2l = {
          type = "app";
          program = "${poetryApp}/bin/s2l";
        };
        pytest = {
          type = "app";
          program = "${poetryEnv}/bin/pytest";
        };
        default = s2l;
      };

      inherit formatter;
    };
}
