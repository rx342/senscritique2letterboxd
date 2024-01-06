{
  description = "senscritique2letterboxd flake";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        poetryEnv = pkgs.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
          preferWheels = true;
        };
      in
      {
        apps.default = {
          type = "app";
          program = ./main.py;
        };

        devShell = pkgs.mkShell {
          nativeBuildInputs = [
            poetryEnv
          ];
        };
      }
    );
}
