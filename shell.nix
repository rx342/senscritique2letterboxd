{
  source ? import ./npins,
  system ? builtins.currentSystem,
  pkgs ? import source.nixpkgs {
    overlays = [ ];
    config = { };
    inherit system;
  },
  pyproject-nix ? import source.pyproject-nix {
    inherit (pkgs) lib;
  },
  uv2nix ? import source.uv2nix {
    inherit (pkgs) lib;
    inherit pyproject-nix;
  },
  pyproject-build-systems ? import source.pyproject-build-systems {
    inherit (pkgs) lib;
    inherit pyproject-nix uv2nix;
  },
}:

let
  workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };
  python = pkgs.python3;
  overlay = workspace.mkPyprojectOverlay {
    sourcePreference = "wheel";
  };
  baseSet = pkgs.callPackage pyproject-nix.build.packages {
    inherit python;
  };
  pythonSet = baseSet.overrideScope (
    pkgs.lib.composeManyExtensions [
      pyproject-build-systems.default
      overlay
    ]
  );
  venv = pythonSet.mkVirtualEnv "s2l" workspace.deps.all;
in
pkgs.mkShellNoCC {
  packages = [
    pkgs.uv
    venv
  ];
}
