cmake_minimum_required(VERSION 3.5)
project(industrial_project)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch config maps
  DESTINATION share/${PROJECT_NAME}
)

file(GLOB_RECURSE traffic_editor_paths "maps/*.building.yaml")

foreach(path ${traffic_editor_paths})
  string(REGEX REPLACE "\\.[^.]*\\.[^.]*$" "" no_extension_path ${path})
  string(REGEX MATCH "[^/]+$" world_name ${no_extension_path})

  set(output_dir ${CMAKE_CURRENT_BINARY_DIR}/maps/${world_name})
  set(output_world_path ${output_dir}/${world_name}.world)
  set(output_world_models_dir ${output_dir}/${world_name}_world)
  set(output_nav_graphs_dir ${output_dir}/nav_graphs)
  set(output_nav_graphs_phony ${output_nav_graphs_dir}/phony)

  file(MAKE_DIRECTORY ${output_dir})
  file(MAKE_DIRECTORY ${output_world_models_dir})
  file(MAKE_DIRECTORY ${output_nav_graphs_dir})

  add_custom_command(
    OUTPUT ${output_world_path}
    COMMAND ros2 run rmf_building_map_tools building_map_generator
      gazebo ${path} ${output_world_path} ${output_world_models_dir}
    DEPENDS ${path}
  )

  add_custom_target(
    generate_${world_name}_world ALL
    DEPENDS ${output_world_path}
  )

  add_custom_command(
    OUTPUT ${output_nav_graphs_phony}
    COMMAND ros2 run rmf_building_map_tools building_map_generator
      nav ${path} ${output_nav_graphs_dir}
    COMMAND ${CMAKE_COMMAND} -E touch ${output_nav_graphs_phony}
    DEPENDS ${path}
  )

  add_custom_target(
    generate_${world_name}_nav_graphs ALL
    DEPENDS ${output_nav_graphs_phony}
  )

  install(
    DIRECTORY ${output_dir}
    DESTINATION share/${PROJECT_NAME}/maps
  )
endforeach()

ament_package()
