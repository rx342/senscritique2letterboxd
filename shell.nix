{
  source ? import ./npins,
  system ? builtins.currentSystem,
  pkgs ? import source.nixpkgs {
    overlays = [ ];
    config = { };
    inherit system;
  },
  poetry2nix ? import source.poetry2nix { inherit pkgs; },
}:

let
  env = poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    preferWheels = true;
  };
in
pkgs.mkShellNoCC {
  packages = [
    pkgs.poetry
    env
  ];
}
