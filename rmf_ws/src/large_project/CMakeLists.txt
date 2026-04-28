cmake_minimum_required(VERSION 3.8)

project(large_project)

find_package(ament_cmake REQUIRED)

# Ponlo en OFF si quieres que durante el build descargue modelos automáticamente
option(NO_DOWNLOAD_MODELS "Do not download Gazebo models during build" ON)

install(DIRECTORY
  launch
  config
  maps
  DESTINATION share/${PROJECT_NAME}
)

file(GLOB_RECURSE building_yaml_paths
  RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}
  "maps/*.building.yaml"
)

foreach(rel_path ${building_yaml_paths})

  set(map_path ${CMAKE_CURRENT_SOURCE_DIR}/${rel_path})

  get_filename_component(world_name ${map_path} NAME_WE)
  string(REPLACE ".building" "" world_name ${world_name})

  set(output_dir ${CMAKE_CURRENT_BINARY_DIR}/maps/${world_name})
  set(output_world_path ${output_dir}/${world_name}.world)
  set(output_model_dir ${output_dir}/models)
  set(output_nav_graphs_dir ${output_dir}/nav_graphs)
  set(output_nav_graphs_stamp ${output_nav_graphs_dir}/.generated)

  # Generar world de Gazebo
  if(NO_DOWNLOAD_MODELS)
    add_custom_command(
      OUTPUT ${output_world_path}
      COMMAND ${CMAKE_COMMAND} -E make_directory ${output_dir}
      COMMAND ros2 run rmf_building_map_tools building_map_generator
              gazebo ${map_path} ${output_world_path} ${output_model_dir}
      DEPENDS ${map_path}
      VERBATIM
    )
  else()
    add_custom_command(
      OUTPUT ${output_world_path}
      COMMAND ${CMAKE_COMMAND} -E make_directory ${output_dir}
      COMMAND ros2 run rmf_building_map_tools building_map_generator
              gazebo ${map_path} ${output_world_path} ${output_model_dir}
      COMMAND ros2 run rmf_building_map_tools building_map_model_downloader
              ${map_path} -e ${output_model_dir}
      DEPENDS ${map_path}
      VERBATIM
    )
  endif()

  add_custom_target(generate_${world_name}_world ALL
    DEPENDS ${output_world_path}
  )

  # Generar nav_graphs
  add_custom_command(
    OUTPUT ${output_nav_graphs_stamp}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${output_nav_graphs_dir}
    COMMAND ros2 run rmf_building_map_tools building_map_generator
            nav ${map_path} ${output_nav_graphs_dir}
    COMMAND ${CMAKE_COMMAND} -E touch ${output_nav_graphs_stamp}
    DEPENDS ${map_path}
    VERBATIM
  )

  add_custom_target(generate_${world_name}_nav_graphs ALL
    DEPENDS ${output_nav_graphs_stamp}
  )

  # Instalar lo generado en build
  install(
    DIRECTORY ${output_dir}/
    DESTINATION share/${PROJECT_NAME}/maps/${world_name}
  )

endforeach()

ament_package()
