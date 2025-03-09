{
  source ? import ./npins,
  pkgs ? import source.nixpkgs { },
  poetry2nix ? import source.poetry2nix { inherit pkgs; },
}:

let
  env = poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    preferWheels = true;
  };
in
pkgs.mkShell {
  nativeBuildInputs = [
    pkgs.poetry
    env
  ];
}
