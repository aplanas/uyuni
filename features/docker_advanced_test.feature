# Copyright (c) 2017 SUSE LLC
# Licensed under the terms of the MIT license.

Feature:  Test advanced functionality of content management

 Scenario: Create an Image Store as docker_admin
  Given I am authorized as "docker" with password "docker"
  And I follow "Images" in the left menu
  And I follow "Stores" in the left menu
  And I follow "Create"
  And I enter "docker_admin" as "label"
  And I enter "registry.mgr.suse.de" as "uri"
  And I click on "create-btn"

 Scenario: Create a profile  As docker admin
   Given I am authorized as "docker" with password "docker"
   And I follow "Images" in the left menu
   And I follow "Profiles" in the left menu
   And I follow "Create"
   And I enter "suse_docker_admin" as "label"
   And I select "galaxy-registry" from "imageStore"
   And I select "1-DOCKER-TEST" from "activationKey"
   And I enter "https://gitlab.suse.de/galaxy/suse-manager-containers.git#:test-profile/serverhost" as "path"
   And I click on "create-btn"
