{
  source ? import ./npins,
  pkgs ? import source.nixpkgs { },
  poetry2nix ? import source.poetry2nix { inherit pkgs; },
}:

poetry2nix.mkPoetryApplication {
  projectDir = ./.;
  preferWheels = true;
}
